from rest_framework import generics, permissions
from .models import Expense
from .serializers import ExpenseSerializer
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth

class ExpenseCreateView(generics.CreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseListView(generics.ListAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        start = self.request.query_params.get('start_date')
        end = self.request.query_params.get('end_date')
        qs = Expense.objects.filter(user=user)
        if start and end:
            qs = qs.filter(date__range=[start, end])
        return qs

class ExpenseAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        expenses = Expense.objects.filter(user=user)

        total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        category = expenses.values('category').annotate(total=Sum('amount'))
        daily = expenses.annotate(day=TruncDay('date')).values('day').annotate(total=Sum('amount'))
        weekly = expenses.annotate(week=TruncWeek('date')).values('week').annotate(total=Sum('amount'))
        monthly = expenses.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount'))

        return Response({
            'total_expense': total,
            'category_breakdown': category,
            'daily_trends': daily,
            'weekly_trends': weekly,
            'monthly_trends': monthly
        })



# Create your views here.
