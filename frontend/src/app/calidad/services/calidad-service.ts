import { Injectable, resource } from '@angular/core';
import { sleep } from '../../core/utils/asyncUtils';
import { datoControl, datoDispersion, datoHistograma, datoPareto } from '../models/graficas';
import { httpResource } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CalidadService {
  private readonly apiUrl = environment.apiUrl

  readonly datosHistograma = httpResource(
    () => `${this.apiUrl}/calidad/histograma`,
    {
      parse: data => datoHistograma.array().parse(data),
      defaultValue: []
    }
  )

  readonly datosPareto = httpResource(
    () => `${this.apiUrl}/calidad/pareto`,
    {
      parse: data => datoPareto.array().parse(data),
      defaultValue: []
    }
  )

  readonly datosDispersion = httpResource(
    () => `${this.apiUrl}/calidad/dispersion`,
    {
      parse: data => datoDispersion.array().parse(data),
      defaultValue: []
    }
  )

  readonly datosControl = httpResource(
    () => `${this.apiUrl}/calidad/control`,
    {
      parse: data => datoControl.array().parse(data),
      defaultValue: []
    }
  )
}
