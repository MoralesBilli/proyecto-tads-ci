import { Component, computed, input, signal } from '@angular/core';
import { ChartData } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import { toSortedAsc } from '../../../core/utils/arrayUtils';

@Component({
  selector: 'app-histograma',
  imports: [BaseChartDirective],
  templateUrl: './histograma.html',
  styleUrl: './histograma.css',
})
export class Histograma<T> {
  readonly data = input.required<T[]>()
  readonly getX = input.required<(item: T) => number>()
  readonly getY = input.required<(item: T) => number>()


  protected readonly chartData = computed<ChartData<'bar'>>(() => {
    const dataOrdenada = toSortedAsc(this.data(), dato => this.getX()(dato))

    return {
      labels: dataOrdenada.map(dato => this.getX()(dato)),
      datasets: [
        { data: dataOrdenada.map(dato => this.getY()(dato)), label: 'Alumnos por Calificación', type: 'bar' },
      ]
    }
  })
}
