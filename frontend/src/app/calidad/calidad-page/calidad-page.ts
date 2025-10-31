import { Component, inject, signal } from '@angular/core';
import { LayoutService } from '../../core/services/layout-service';
import { TiposDeGrafica } from '../components/tipos-de-grafica/tipos-de-grafica';
import { Histograma } from '../components/histograma/histograma';
import { Pareto } from '../components/pareto/pareto';
import { Dispersion } from '../components/dispersion/dispersion';
import { Control } from '../components/control/control';
import { CalidadService } from '../services/calidad-service';
import { DatoControl, DatoDispersion, DatoHistograma, DatoPareto } from '../models/graficas';

@Component({
  selector: 'app-calidad-page',
  imports: [TiposDeGrafica, Histograma, Pareto, Dispersion, Control],
  templateUrl: './calidad-page.html',
  styleUrl: './calidad-page.css',
})
export class CalidadPage {
  private readonly calidadService = inject(CalidadService)

  constructor(private titleService: LayoutService) {
    this.titleService.title.set('Calidad');
  }

  graficaSeleccionada = signal('')

  protected readonly datosHistograma = this.calidadService.datosHistograma
  protected readonly getHistogramaX = (dato: DatoHistograma) => dato.calificacion
  protected readonly getHistogramaY = (dato: DatoHistograma) => dato.qty

  protected readonly datosPareto = this.calidadService.datosPareto
  protected readonly getParetoX = (dato: DatoPareto) => dato.factor
  protected readonly getParetoY = (dato: DatoPareto) => dato.qty

  protected readonly datosDispersion = this.calidadService.datosDispersion
  protected readonly getDispersionX = (dato: DatoDispersion) => dato.faltas
  protected readonly getDispersionY = (dato: DatoDispersion) => dato.calificacion

  protected readonly datosControl = this.calidadService.datosControl
  protected readonly getControlX = (dato: DatoControl) => dato.unidad
  protected readonly getControlY = (dato: DatoControl) => dato.calificacionPromedio
}
