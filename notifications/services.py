from datetime import datetime

from sqlalchemy.orm import Session
from db import models
from notifications import schemas


class NotificationService:
    @staticmethod
    def get_all_flight_on_sale(db: Session):
        return db.query(models.Flight, models.FlightGuide).filter(
            models.Flight.on_sale <= datetime.utcnow(),
        ).join(
            models.FlightGuide, models.FlightGuide.id == models.Flight.flight_guide_id
        ).order_by(models.Flight.on_sale.desc()).first()

    @staticmethod
    def get_all_admins_user_ids(db: Session):
        return db.query(models.User.id).filter(
            models.User.role_id == 2).all()

    @staticmethod
    def set_notification(db: Session, user_id: int, message: str, action: str):
        db.add(models.UserNotification(user_id=user_id, message=message, is_read=False, action=action))
        db.commit()

    @staticmethod
    def get_start_sale_flights(db: Session):
        """
        Get flight that are on sale and add notification to admins
        """
        flights = NotificationService.get_all_flight_on_sale(db)
        admins = NotificationService.get_all_admins_user_ids(db)
        last_notification = db.query(models.UserNotification). \
            filter(models.UserNotification.action == "start_sale").order_by(models.UserNotification.id.desc()).first()

        if flights is not None and admins is not None:
            notification = {
                "message": {
                    "show": f"Flight start sale {flights[1].flight_number} departure time is"
                            f" {flights[0].departure_date.strftime('%d-%m-%Y %H:%M')}",
                    "flight_number": flights[1].flight_number,
                    "departure_date": f"{flights[0].departure_date}",
                }
            }

            if last_notification is None:
                for admin in admins:
                    NotificationService.set_notification(db, admin[0], str(notification), "start_sale")
            elif last_notification is not None:
                msg = eval(last_notification.message)
                if msg['message']['flight_number'] != notification['message']['flight_number'] and \
                        msg['message']['departure_date'] != notification['message']['departure_date']:
                    for admin in admins:
                        NotificationService.set_notification(db, admin[0], str(notification), "start_sale")

    @staticmethod
    def get_notifications(db: Session, page: int, limit: int):
        NotificationService.get_start_sale_flights(db)
        query = db.query(models.UserNotification).filter(models.UserNotification.is_read == False)
        if page and limit:
            return query.offset(limit * (page - 1)).limit(limit).all()
        return query.all()

    @staticmethod
    def update_notification(db: Session, notification: schemas.NotificationUpdate):
        db.query(models.UserNotification).filter(models.UserNotification.id == notification.id). \
            update({"is_read": notification.is_read})
        db.commit()
        return db.query(models.UserNotification).filter(models.UserNotification.id == notification.id).first()