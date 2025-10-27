import { Component, ElementRef, inject, viewChild } from '@angular/core';
import { ToastService } from '../../../core/services/toast-service';

@Component({
  selector: 'app-alumnos-fab',
  imports: [],
  templateUrl: './alumnos-fab.html',
  styleUrl: './alumnos-fab.css',
})
export class AlumnosFab {
  private fileImportarAlumnos = viewChild.required<ElementRef<HTMLInputElement>>('fileImportarAlumnos');
  private fileImportarCalificaciones = viewChild.required<ElementRef<HTMLInputElement>>('fileImportarCalificaciones');

  private toastService = inject(ToastService);

  protected handleExportarAlumnos() {
    if (Math.random() < 0.5) {
      this.toastService.show('Error al exportar alumnos', 'error');
    }
    else {
      this.toastService.show('Alumnos exportados exitosamente', 'success')
    }
  }

  protected handleImportarAlumnos() {
    this.fileImportarAlumnos().nativeElement.click()
  }

  protected handleAlumnosImportados(event: Event) {
    const files = this.fileImportarAlumnos().nativeElement.files;

    if (files && files.length > 0) {
      this.toastService.show(`Alumnos importados desde ${files[0].name}`, 'success');
    }
    else {
      this.toastService.show('No se seleccionó ningún archivo', 'warning');
    }
  }

  protected handleImportarCalificaciones() {
    this.fileImportarCalificaciones().nativeElement.click()
  }

  protected handleCalificacionesImportados(event: Event) {
    const files = this.fileImportarCalificaciones().nativeElement.files;

    if (files && files.length > 0) {
      this.toastService.show(`Calificaciones importadas desde ${files[0].name}`, 'success');
    }
    else {
      this.toastService.show('No se seleccionó ningún archivo', 'warning');
    }
  }
}
