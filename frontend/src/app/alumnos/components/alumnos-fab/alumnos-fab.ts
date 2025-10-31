import { Component, ElementRef, inject, viewChild } from '@angular/core';
import { ToastService } from '../../../core/services/toast-service';
import { AlumnosService } from '../../services/alumnos-service';
import { catchError, finalize, of, tap } from 'rxjs';

@Component({
  selector: 'app-alumnos-fab',
  imports: [],
  templateUrl: './alumnos-fab.html',
  styleUrl: './alumnos-fab.css',
})
export class AlumnosFab {
  private fileImportarAlumnos = viewChild.required<ElementRef<HTMLInputElement>>('fileImportarAlumnos');
  private fileImportarCalificaciones = viewChild.required<ElementRef<HTMLInputElement>>('fileImportarCalificaciones');

  private alumnosService = inject(AlumnosService);
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
      this.alumnosService.importarAlumnos(files[0]).pipe(
        tap(() => {
          this.toastService.show(`Alumnos importados desde ${files[0].name}`, 'success');
        }),
        catchError((err) => {
          this.toastService.show(err.error.error, 'error');
          return of(null)
        }),
        finalize(() => {
          this.fileImportarAlumnos().nativeElement.value = '';
          this.alumnosService.alumnos.reload()
        })

      )
      .subscribe()
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
      this.alumnosService.importarCalificaciones(files[0]).pipe(
        tap(() => {
          this.toastService.show(`Calificaciones importadas desde ${files[0].name}`, 'success');
        }),
        catchError((err) => {
          this.toastService.show(err.error.error, 'error');
          return of(null);
        }),
        finalize(() => {
          this.fileImportarCalificaciones().nativeElement.value = '';
          this.alumnosService.alumnoSeleccionadoDetalle.reload()
        })
      )
      .subscribe()
    }
    else {
      this.toastService.show('No se seleccionó ningún archivo', 'warning');
    }
  }
}
