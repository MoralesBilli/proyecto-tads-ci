import { ChangeDetectionStrategy, Component, computed, input, signal } from '@angular/core';
import { BaseChartDirective } from 'ng2-charts';
import { toSortedDesc } from '../../../core/utils/arrayUtils';
import { ChartData, ChartOptions } from 'chart.js';

@Component({
  selector: 'app-pareto',
  imports: [BaseChartDirective],
  templateUrl: './pareto.html',
  styleUrl: './pareto.css',
})
export class Pareto<T> {
  readonly data = input.required<T[]>()
  readonly getX = input.required<(item: T) => unknown>()
  readonly getY = input.required<(item: T) => number>()

  protected readonly total = computed(() =>
    this.data().reduce((acum, item) => acum + this.getY()(item), 0)
  );

  private getAcumulatedData(data: T[]): number[] {
    const acumulated: number[] = [];
    let acum = 0

    for (const item of data) {
      acum += this.getY()(item);
      acumulated.push(acum);
    }

    return acumulated;
  }

  protected readonly chartData = computed<ChartData<'bar' | 'line'>>(() => {
    const dataOrdenada = toSortedDesc(this.data(), dato => this.getY()(dato))
    const dataAcum = this.getAcumulatedData(dataOrdenada);

    return {
      labels: dataOrdenada.map(dato => this.getX()(dato)),
      datasets: [
        {
          data: dataOrdenada.map(dato => this.getY()(dato)),
          label: 'Alumnos por factor',
          type: 'bar',
          yAxisID: 'cantidad'
        },
        {
          data: dataAcum,
          label: 'Acumulado',
          type: 'line',
          yAxisID: 'porcentaje',
          fill: false,
          tension: 0.2
        }
      ]
    }
  })

  protected readonly chartOptions = computed<ChartOptions<'bar' | 'line'>>(() => {
    const total = this.total();

    const axisMax = total > 0 ? total + 10 : 1;
    const tickValues = total === 0
      ? [0]
      : [0, 0.2, 0.4, 0.6, 0.8, 1].map(step => Number((total * step).toFixed(4)));

    return {
      responsive: true,
      scales: {
        cantidad: {
          beginAtZero: true,
          position: 'left',
          max: axisMax,
          title: { display: true, text: 'Cantidad de alumnos' },
          grid: { drawOnChartArea: false }
        },
        porcentaje: {
          beginAtZero: true,
          position: 'right',
          min: 0,
          max: axisMax,
          afterBuildTicks: scale => {
            scale.ticks = tickValues.map(value => ({ value }));
          },
          ticks: {
            callback: value => {
              const numericValue = Number(value);
              if (!Number.isFinite(numericValue) || total === 0) {
                return '0%';
              }
              const percent = (numericValue / total) * 100;
              return `${percent.toFixed(0)}%`;
            }
          },
          title: { display: true, text: 'Porcentaje acumulado' }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: context => {
              if (context.dataset.yAxisID === 'porcentaje') {
                const valor = Number(context.parsed.y);
                const percent = total === 0 ? 0 : (valor / total) * 100;
                return `${context.dataset.label}: ${percent.toFixed(1)}%`;
              }
              return `${context.dataset.label}: ${context.parsed.y}`;
            }
          }
        }
      }
    };
  })
}
