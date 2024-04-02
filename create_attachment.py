from file_storage.models import Plan, Attachment

all_plans = Plan.objects.all()

for plan in all_plans:  
    if plan.attachment.name != '':
        new_attachment = Attachment(
            name=plan.attachment.name,
            file=plan.attachment,
            plan = plan
        )
        new_attachment.save()
        print(plan.attachment.name)
