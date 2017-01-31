from django.contrib import admin
from app.models import *


# ============  Label   ====================================================
admin.site.register(Label)
# ==========================================================================

# ============  ClientCategory  ============================================
admin.site.register(ClientCategory)
# ==========================================================================


# ============  Client  ====================================================
class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1


class ClientAdmin(admin.ModelAdmin):
    date_hierarchy = 'init_date'
    fields = [
        'user',
        'name',
        'full_name',
        'balance',
        'category',
        'address',
        'phone',
        'fop',
        'code_ipn',
        'code_1c',
        'email_verified',
        'overall_mark',
        'deprecated',
    ]
    readonly_fields = ['email_verified']
    inlines = [ReviewInline]

admin.site.register(Client, ClientAdmin)
# ==========================================================================


# ============  ApplicationStatus  =========================================
admin.site.register(ApplicationStatus)
# ==========================================================================

# ============  ApplicationType  ===========================================
admin.site.register(ApplicationType)
# ==========================================================================

# ============  Resolution  ================================================
admin.site.register(Resolution)
# ==========================================================================


# ============  Application  ===============================================
class ApplicationScanInlite(admin.StackedInline):
    model = ApplicationScan
    extra = 1


class ApplicationAttachmentInline(admin.StackedInline):
    model = ApplicationAttachment
    extra = 1


class ApplicationMessageInline(admin.StackedInline):
    model = ApplicationMessage
    extra = 1


class ApplicationControlInline(admin.StackedInline):
    model = ApplicationControl
    extra = 1


class ApplicationHistoryInline(admin.StackedInline):
    model = ApplicationHistory
    extra = 1


class ApplicationAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    inlines = [
        ApplicationScanInlite,
        ApplicationAttachmentInline,
        ApplicationMessageInline,
        ApplicationControlInline,
        ApplicationHistoryInline,
    ]

admin.site.register(Application, ApplicationAdmin)
# ==========================================================================


# ============  Department  ================================================
class DepartmentEmployeeInline(admin.StackedInline):
    model = DepartmentEmployee
    extra = 1


class SubmissionInline(admin.StackedInline):
    model = Submission
    fk_name = 'parent_department'
    fields = ['child_department']
    extra = 1


class DepartmentHeadInline(admin.StackedInline):
    model = DepartmentHead
    extra = 1
    max_num = 1


class DepartmentAdmin(admin.ModelAdmin):
    inlines = [
        DepartmentHeadInline,
        DepartmentEmployeeInline,
        SubmissionInline,
    ]

admin.site.register(Department, DepartmentAdmin)
# ==========================================================================


# ============  Employee  ==================================================
class EmployeeDepartmentInline(admin.StackedInline):
    model = DepartmentEmployee
    extra = 1
    max_num = 1


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = ['email_verified']
    # inlines = [
    #     # EmployeeRoleInlile,
    #     # EmployeeDepartmentInline,
    # ]

# admin.site.register(Employee, EmployeeAdmin)
# ==========================================================================

# ============  Submission  ================================================
admin.site.register(Submission)
# ==========================================================================

# ============  Role  ======================================================
# admin.site.register(Role)
# ==========================================================================

# ============  DepartmentHead  ============================================
# admin.site.register(DepartmentHead)
# ==========================================================================

# ============  DepartmentEmployee  ========================================
# admin.site.register(DepartmentEmployee)
# ==========================================================================

# ============  ResponseType  ==============================================
admin.site.register(ResponseType)
# ==========================================================================

# ============  Mark  ======================================================
admin.site.register(Mark)
# ==========================================================================


# ============  Response  ==================================================
class ResponseScanInline(admin.StackedInline):
    model = ResponseScan
    extra = 1


class ResponseAttachmentInline(admin.StackedInline):
    model = ResponseAttachment
    extra = 1


class ResponseBillInline(admin.StackedInline):
    model = ResponseBill
    extra = 1


class ResponsePerformerInline(admin.StackedInline):
    model = ResponsePerformer
    extra = 1


class ResponseAdmin(admin.ModelAdmin):
    inlines = [
        ResponsePerformerInline,
        ResponseScanInline,
        ResponseAttachmentInline,
        ResponseBillInline,
    ]

admin.site.register(Response, ResponseAdmin)
# ==========================================================================
