import { Component, computed, input, output } from '@angular/core';
import { Alumno } from '../../models/alumnoSchema';
import { toSortedDesc } from '../../../core/utils/arrayUtils';

const formatter = new Intl.ListFormat('es', { style: 'long', type: 'conjunction' });

@Component({
  selector: 'app-alumnos-list',
  imports: [],
  templateUrl: './alumnos-list.html',
  styleUrl: './alumnos-list.css',
})
export class AlumnosList {
  public readonly alumnos = input.required<Alumno[]>();
  public readonly alumnoSeleccionado = input<Alumno|null>(null);

  public readonly alumnoSeleccionadoChange = output<Alumno>();

  protected readonly alumnosOrdenados = computed(() => {
    return toSortedDesc(this.alumnos(), alumno => alumno.factoresDeRiesgo.length);
  })

  protected handleAlumnoSeleccionadoChange(alumno: Alumno): void {
    this.alumnoSeleccionadoChange.emit(alumno);
  }

  protected getFactoresDeRiesgo(alumno: Alumno): string {
    return formatter.format(alumno.factoresDeRiesgo);
  }

  protected getBadgeColor(alumno: Alumno): string {
    if (alumno.factoresDeRiesgo.length === 0) return 'badge-neutral'
    if (alumno.factoresDeRiesgo.length < 3) return 'badge-warning'
    return 'badge-error'
  }
}
