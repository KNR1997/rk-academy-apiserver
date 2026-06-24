from academy.app.serializers.base import BaseSerializer
from academy.db.models import EnrollmentCharge
from academy.app.serializers.enrollment import EnrollmentListSerializer


class EnrollmentChargeListSerializer(BaseSerializer):
    enrollment = EnrollmentListSerializer()

    class Meta:
        model = EnrollmentCharge
        fields = [
            'id',
            'amount',
            'billing_month',
            'billing_year',
            'status',
            'enrollment'
        ]
