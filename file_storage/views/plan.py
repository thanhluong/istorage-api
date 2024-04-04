from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication

from file_storage.serializers import PlanSerializer, AttachmentSerializer

from file_storage.models import Plan
from file_storage.models import GovFile, PlanNLLSApprover, StorageUser, Organ, PlanNLLSOrgan
from file_storage.models import Attachment

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class PlanListView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        plans = Plan.objects.all()
        if request.user.is_authenticated:
            if (not request.user.is_superuser) and request.user.department and request.user.department.organ:
                organ_id = request.user.department.organ.id
                plans = plans.filter(organ__id=organ_id)

        for plan in plans:
            attachment = Attachment.objects.filter(plan=plan)
            plan.attachments = attachment
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer_plan = PlanSerializer(data={
            "organ": request.data.get("organ"),
            "name": request.data.get("name"),
            "state": request.data.get("state"),
            "type": request.data.get("type"),
        })
        if serializer_plan.is_valid():
            plan_instance = serializer_plan.save()  # Save the plan instance
            idx = 0
            while f'attachment{idx}' in request.data:
                serializer = AttachmentSerializer(data={
                    "file": request.data[f'attachment{idx}'],
                    "plan": plan_instance.pk,  # Use the primary key of the plan instance
                })
                if serializer.is_valid():
                    serializer.save()
                else:
                    plan_instance.delete()  # Delete the plan instance if attachment serializer is not valid
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                idx += 1
        return Response(serializer_plan.errors, status=status.HTTP_200_OK)


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
        attachment = Attachment.objects.filter(plan_id=plan_id)
        plan.attachments = attachment
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
        print("hello from get plan")
        plans = Plan.objects.filter(type=plan_type)
        if request.user.is_authenticated:
            if (not request.user.is_superuser) and request.user.department and request.user.department.organ:
                organ_id = request.user.department.organ.id
                plans = plans.filter(organ__id=organ_id)

        for plan in plans:
            attachments = Attachment.objects.filter(plan=plan)
            plan.attachments = attachments
        serializer = PlanSerializer(plans, many=True)
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
    authentication_classes = (CsrfExemptSessionAuthentication,)
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
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        sender = StorageUser.objects.get(id=request.data['sender_id'])
        plan_ids = request.data['plan_ids']
        organ_ids = request.data['organ_ids']
        organ_sender = Organ.objects.get(id = request.data['organ_sender_id'])
        for plan_id in plan_ids:
            plan = Plan.objects.get(id=plan_id)

            for organ_id in organ_ids:
                organ = Organ.objects.get(id=organ_id)

                exist_plan = PlanNLLSOrgan.objects.filter(
                    plan=plan,
                    sender=sender,
                    organ=organ,
                    organ_sender=organ_sender,
                )

                if exist_plan.exists():
                    return Response({"message": f"Plan {plan_id} for Organ {organ_id} already exists"}, status=status.HTTP_200_OK)

                PlanNLLSOrgan.objects.create(
                    sender=sender,
                    plan=plan,
                    organ=organ,
                    organ_sender=organ_sender,
                )

        return Response({"message": "Send plan success"}, status=status.HTTP_200_OK)

class NLLSInternal(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, id):
        plans_nlls_approvers = PlanNLLSApprover.objects.filter(approver_id=id)
        plans = []
        for plans_nlls_approver in plans_nlls_approvers:
            plan = Plan.objects.get(id=plans_nlls_approver.plan.id)
            attachments = Attachment.objects.filter(plan_id=id)
            plan.attachments = attachments
            plans.append(plan)
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SentNLLSInternal(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.AllowAny,)
    def get(self, request, sender_id):
        plans_nlls_organs = PlanNLLSOrgan.objects.filter(sender_id=sender_id)
        distinct_plans_ids = plans_nlls_organs.values('plan_id').distinct()
        plans = Plan.objects.filter(id__in=distinct_plans_ids)
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class NLLSOrganByOrganId(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, id):
        plans_nlls_organ = PlanNLLSOrgan.objects.filter(organ_id=id)
        plans = []
        for plan_nlls_organ in plans_nlls_organ:
            plan = Plan.objects.get(id=plan_nlls_organ.plan.id)
            attachments = Attachment.objects.filter(plan_id=id)
            plan.attachments = attachments
            plans.append(plan)
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class NLLSOrgan(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        organ_sender_id = request.GET.get('organ_sender_id')
        plans_nlls_organ = PlanNLLSOrgan.objects.filter(organ_sender_id=organ_sender_id)
        plans = []
        for plan_nlls_organ in plans_nlls_organ:
            plan = Plan.objects.get(id=plan_nlls_organ.plan.id)
            attachments = Attachment.objects.filter(plan_id=id)
            plan.attachments = attachments
            plans.append(plan)
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


