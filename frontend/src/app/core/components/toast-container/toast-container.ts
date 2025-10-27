import { Component, inject } from '@angular/core';
import { ToastService } from '../../services/toast-service';

@Component({
  selector: 'app-toast-container',
  imports: [],
  templateUrl: './toast-container.html',
  styleUrl: './toast-container.css',
})
export class ToastContainer {
  private readonly toastService = inject(ToastService);
  protected readonly toasts = this.toastService.toasts;

  protected getToastPath(type: string): string {
    return ''
  }

  protected getToastClass(type: string): string {
    switch (type) {
      case 'success': return 'alert-success';
      case 'error': return 'alert-error';
      case 'info': return 'alert-info';
      case 'warning': return 'alert-warning';
      default: return '';
    }
  }
}
