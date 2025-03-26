from django.contrib import admin
from . import models
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def export_to_pdf(modeladmin, request, queryset):
    # Create a new PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # Generate the report using ReportLab
    doc = SimpleDocTemplate(response, pagesize=letter)

    elements = []

    # Define the style for the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Create the table headers
    headers = ['user_name', "monument_name", "guide_name", "total", "date"]

    # Create the table data
    data = []
    for obj in queryset:
        data.append([obj.user_name, obj.monument_name, obj.guide_name, obj.charges, obj.booked_time])

    # Create the table
    t = Table([headers] + data, style=style)

    # Add the table to the elements array
    elements.append(t)

    # Build the PDF document
    doc.build(elements)

    return response


export_to_pdf.short_description = "Export to PDF"


# Register your models here.

# class showadmin(admin.ModelAdmin):
#     list_display = ["name","email_id","password"]

class showuser(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ["user_photo", "name", "email_id", "citys", "password"]


class showcity(admin.ModelAdmin):
    list_display = ["city_name"]


class showmonument(admin.ModelAdmin):
    list_display = ["monument_name", "admin_photo", "contact_no", "charges", "category"]


class showmonumentimages(admin.ModelAdmin):
    list_display = ['monument', 'admin_photo']


class showpayment(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ["user_name", "monument_name", "guide_name", "total", "date", "payment_type"]
    list_filter = ["date"]
    actions = [export_to_pdf]


class showfeedback(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ["user_name", "monument_name", "comment", "date", "rating"]

class showaudio(admin.ModelAdmin):
    list_display = ["monument_name", "file_path_english", "file_path_gujarati", "file_path_hindi"]


class showcontact(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ["name", "phone", "message", "date"]

class showcategory(admin.ModelAdmin):
    list_display = ["cat_name"]


# admin.site.register(models.admin_model,showadmin)
admin.site.register(models.user, showuser)
admin.site.register(models.city, showcity)
admin.site.register(models.monument, showmonument)
admin.site.register(models.payment, showpayment)
admin.site.register(models.feedback, showfeedback)
admin.site.register(models.audio, showaudio)
admin.site.register(models.contact, showcontact)
admin.site.register(models.category, showcategory)
admin.site.register(models.monument_photos, showmonumentimages)
