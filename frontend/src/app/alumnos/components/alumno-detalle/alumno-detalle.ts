import { Component, computed, input } from '@angular/core';
import { AlumnoDetalle as AlumnoDetalleModel } from '../../models/alumnoDetalleSchema';

@Component({
  selector: 'app-alumno-detalle',
  imports: [],
  templateUrl: './alumno-detalle.html',
  styleUrl: './alumno-detalle.css'
})
export class AlumnoDetalle {
  readonly detalle = input<AlumnoDetalleModel | null>(null);

  protected readonly inscripciones = computed(() => this.detalle()?.inscripciones ?? []);

  protected readonly promedioCalificaciones = computed(() => {
    const detalle = this.detalle();
    if (!detalle) return null;
    const calificaciones = detalle.inscripciones.flatMap(inscripcion => inscripcion.calificaciones);
    if (calificaciones.length === 0) return null;
    const total = calificaciones.reduce((sum, item) => sum + item.calificacion, 0);
    return Math.round((total / calificaciones.length) * 10) / 10;
  });

  protected readonly promedioCalificacionesTexto = computed(() => {
    const promedio = this.promedioCalificaciones();
    return promedio === null ? 'N/A' : promedio.toFixed(1);
  });

  protected readonly totalFaltas = computed(() => {
    const detalle = this.detalle();
    if (!detalle) return 0;
    return detalle.inscripciones.reduce((sum, inscripcion) => {
      return sum + inscripcion.calificaciones.reduce((faltas, unidad) => faltas + unidad.faltas, 0);
    }, 0);
  });
}
