from django.db import transaction
from rest_framework.exceptions import ValidationError
from apps.orders.models import Order

class OrderService:

    @staticmethod
    def create_order(product, buyer, notes=""):

        if product.status == "SOLD":
            raise ValidationError("Mahsulot allaqachon sotilgan.")

        if product.seller == buyer:
            raise ValidationError("O'zingizning mahsulotingizni sotib olmaysiz.")

        if Order.objects.filter(
            product=product,
            buyer=buyer,
            status__in=[Order.Status.WAITING, Order.Status.AGREED]
        ).exists():
            raise ValidationError("Siz allaqachon buyurtma bergansiz.")

        return Order.objects.create(
            product=product,
            buyer=buyer,
            seller=product.seller,
            final_price=product.price,
            notes=notes
        )

    @staticmethod
    @transaction.atomic
    def change_status(order, user, new_status, data):

        if user != order.seller and user != order.buyer:
            raise ValidationError("Ruxsat yo'q.")

        if user == order.seller:
            if order.status != Order.Status.WAITING:
                raise ValidationError("Faqat WAITING holatda o'zgartira olasiz.")

            if new_status not in [Order.Status.AGREED, Order.Status.REJECT]:
                raise ValidationError("Noto'g'ri status.")

            if new_status == Order.Status.AGREED:
                if not data.get("meeting_location"):
                    raise ValidationError("Uchrashuv joyi majburiy.")

                order.meeting_location = data.get("meeting_location")
                order.meeting_time = data.get("meeting_time")
                order.final_price = data.get("final_price", order.final_price)

        if user == order.buyer:
            if order.status != Order.Status.AGREED:
                raise ValidationError("Faqat AGREED holatda o'zgartira olasiz.")

            if new_status not in [Order.Status.PURCHASED, Order.Status.REJECT]:
                raise ValidationError("Noto'g'ri status.")

        order.status = new_status
        order.save()

        if new_status == Order.Status.PURCHASED:
            product = order.product

            if product.status == "SOLD":
                raise ValidationError("Mahsulot allaqachon sotilgan.")

            product.status = "SOLD"
            product.save(update_fields=["status"])

            seller = order.seller
            seller.total_sales += 1
            seller.save(update_fields=["total_sales"])

        return order