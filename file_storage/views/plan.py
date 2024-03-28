from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication

from file_storage.serializers import PlanSerializer, OrganSerializer

from file_storage.models import Plan
from file_storage.models import GovFile, PlanNLLSApprover, StorageUser, Organ, PlanNLLSOrgan


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class PlanListView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        plan = Plan.objects.all()

        if request.user.is_authenticated:
            if (not request.user.is_superuser) and request.user.department and request.user.department.organ:
                organ_id = request.user.department.organ.id
                plan = Plan.objects.filter(organ__id=organ_id)

        serializer = PlanSerializer(plan, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlanDetailView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, plan_id, *args, **kwargs):
        try:
            return Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return None

    def get(self, request, plan_id):
        plan = self.get_object(plan_id)
        if plan is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PlanSerializer(plan)
        return Response(serializer.data)

    def put(self, request, plan_id):
        plan = self.get_object(plan_id)
        if plan is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PlanSerializer(plan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, plan_id):
        plan = self.get_object(plan_id)
        if plan is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlanByTypeListView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, plan_type):
        plan = Plan.objects.filter(type=plan_type)

        if request.user.is_authenticated:
            if (not request.user.is_superuser) and request.user.department and request.user.department.organ:
                organ_id = request.user.department.organ.id
                plan = plan.filter(organ__id=organ_id)

        serializer = PlanSerializer(plan, many=True)
        return Response(serializer.data)


class SetPlanView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        gov_file_id = request.data['gov_file_id']
        plan_id = request.data['plan_id']

        gov_file = GovFile.objects.get(id=gov_file_id)
        plan = Plan.objects.get(id=plan_id)
        gov_file.plan_nopluuls = plan
        gov_file.save()
        return Response(status=status.HTTP_200_OK)


class RemovePlanView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        gov_file_id = request.data['gov_file_id']

        gov_file = GovFile.objects.get(id=gov_file_id)
        gov_file.plan_nopluuls = None
        gov_file.save()
        return Response(status=status.HTTP_200_OK)


class SetPlanTieuHuyView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        gov_file_id = request.data['gov_file_id']
        plan_id = request.data['plan_id']

        gov_file = GovFile.objects.get(id=gov_file_id)
        plan = Plan.objects.get(id=plan_id)
        gov_file.plan_tieuhuy = plan
        gov_file.save()
        return Response(status=status.HTTP_200_OK)


class RemovePlanTieuHuyView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        gov_file_id = request.data['gov_file_id']

        gov_file = GovFile.objects.get(id=gov_file_id)
        gov_file.plan_tieuhuy = None
        gov_file.save()
        return Response(status=status.HTTP_200_OK)
    
class SendNLLSInternal(APIView):
    # authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        sender = StorageUser.objects.get(id=request.data['sender_id'])
        approver_ids = request.data['approver_ids']
        plan_ids = request.data['plan_ids']
        
        for plan_id in plan_ids:
            plan = Plan.objects.get(id=plan_id)
            for approver_id in approver_ids:
                approver = StorageUser.objects.get(id=approver_id)
                PlanNLLSApprover.objects.create(
                    sender=sender, 
                    plan=plan,
                    approver=approver
                )
                
        return Response({"message": "Send plan success"}, status=status.HTTP_200_OK)


class SendNLLSOrgan(APIView):
    # authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        sender = StorageUser.objects.get(id=request.data['sender_id'])
        plan_ids = request.data['plan_ids']
        organ_ids = request.data['organ_ids']

        for plan_id in plan_ids:
            plan = Plan.objects.get(id=plan_id)

            for organ_id in organ_ids:
                organ = Organ.objects.get(id=organ_id)

                exist_plan = PlanNLLSOrgan.objects.filter(
                    plan=plan,
                    sender=sender,
                    organ=organ
                )

                if exist_plan.exists():
                    return Response({"message": f"Plan {plan_id} for Organ {organ_id} already exists"}, status=status.HTTP_200_OK)

                PlanNLLSOrgan.objects.create(
                    sender=sender,
                    plan=plan,
                    organ=organ
                )

        return Response({"message": "Send plan success"}, status=status.HTTP_200_OK)

class NLLSInternal(APIView):
    # authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, id):
        plans = PlanNLLSApprover.objects.filter(approver_id=id)
        serialized_plans = []
        for plan in plans:
            serialized_plans.append(PlanSerializer(Plan.objects.get(id=plan.plan.id)).data)
        return Response(serialized_plans, status=status.HTTP_200_OK)

class NLLSOrgan(APIView):
    # authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, id):
        plans = PlanNLLSOrgan.objects.filter(organ_id=id)
        serialized_plans = []
        for plan in plans:
            serialized_plans.append(PlanSerializer(Plan.objects.get(id=plan.plan.id)).data)
        return Response(serialized_plans, status=status.HTTP_200_OK)
