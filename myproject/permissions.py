from django.contrib.auth.mixins import PermissionRequiredMixin
'''
https://www.youtube.com/watch?v=zszYgUXnId8
view the above video for permissions
'''

class TechnicianPermission(PermissionRequiredMixin):
    permission_required = (
                            'patient.view_patient',
                            'patient.add_patient',
                            'patient.change_patient',
                            'patient.delete_patient',
                            'sample.view_sample',
                            'sample.add_sample',
                            'sample.change_sample',
                            'sample.delete_sample',
                          )
    def handle_no_permission(self):
        return render(self.request,'403.html', status=403)

class PostGraduatePermission(TechnicianPermission):
    permission_required = TechnicianPermission.permission_required + (
                            'result.view_result',
                            'result.add_result',
                            'result.change_result',
                            'result.delete_result'
    )

class ProfessorPermission(PostGraduatePermission):
    permission_required = PostGraduatePermission.permission_required + (
        'verification.view_verification',
        'verification.add_verification',
        'verification.change_verification',
        'verification.delete_verification'
    )

class SuperuserPermission(ProfessorPermission):
    permission_required = ProfessorPermission.permission_required + (
        'auth.view_user',
        'auth.add_user',
        'auth.change_user',
        'auth.delete_user'
    )
