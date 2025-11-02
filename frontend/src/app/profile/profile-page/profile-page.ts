import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators, AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';
import { AuthService } from '../../core/services/auth-service';
import { LayoutService } from '../../core/services/layout-service';
import { computed, signal } from '@angular/core';
import { Router } from '@angular/router';
import { getProfilePhoto } from '../../core/utils/photoUtils';
import { ToastService } from '../../core/services/toast-service';

@Component({
  selector: 'app-profile-page',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './profile-page.html',
  styleUrl: './profile-page.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProfilePage {
  private fb = new FormBuilder();
  private readonly layout = inject(LayoutService);

  get decoded() { return this.auth.decoded; }

  get expMs(): number | null {
    const payload = this.decoded();
    const exp = payload?.exp;
    return typeof exp === 'number' ? exp * 1000 : null;
  }

  protected readonly photoUrl = computed(() => {
    const id = this.decoded()?.id;
    if (!id) return '';
    return getProfilePhoto(String(id));
  });

  private passwordStrengthValidator: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
    const value = String(control.value ?? '');
    if (!value) return null; // required handled separately
    const errors: ValidationErrors = {};
    if (!/[A-Z]/.test(value)) errors['uppercase'] = true;
    if (!/\d/.test(value)) errors['digit'] = true;
    return Object.keys(errors).length ? errors : null;
  };

  private passwordsMatchValidator: ValidatorFn = (group: AbstractControl): ValidationErrors | null => {
    const nueva = group.get('nueva_contrasena')?.value;
    const confirmar = group.get('confirmar')?.value;
    if (!nueva || !confirmar) return null; // required handled separately
    return nueva === confirmar ? null : { passwordMismatch: true };
  };

  form = this.fb.group({
    contrasena_actual: ['', [Validators.required]],
    nueva_contrasena: ['', [Validators.required, Validators.minLength(8), this.passwordStrengthValidator]],
    confirmar: ['', [Validators.required]],
  }, { validators: this.passwordsMatchValidator });

  loading = signal(false);


  constructor(private auth: AuthService, private router: Router, private toast: ToastService) {
    this.layout.title.set('Perfil');
  }

  logout() {
    this.auth.logout();
    this.router.navigateByUrl('/login');
  }

  async submit() {
    if (this.form.invalid) return this.form.markAllAsTouched();
    const { contrasena_actual, nueva_contrasena, confirmar } = this.form.value as any;
    if (nueva_contrasena !== confirmar) {
      this.toast.show('Las contraseñas no coinciden', 'error', 5000);
      return;
    }
    this.loading.set(true);
    try {
      await this.auth.changePassword({ contrasena_actual, nueva_contrasena });
      this.toast.show('Contraseña actualizada correctamente', 'success', 4000);
      this.form.reset();
    } catch (e: any) {
      const message = e?.error?.error || e?.error?.message || e?.message || 'No se pudo actualizar la contraseña';
      this.toast.show(message, 'error', 5000);
    } finally {
      this.loading.set(false);
    }
  }
}
