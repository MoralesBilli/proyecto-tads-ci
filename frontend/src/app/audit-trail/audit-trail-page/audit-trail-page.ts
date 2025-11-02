import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuditTrailService } from '../services/audit-trail-service';
import { LayoutService } from '../../core/services/layout-service';

@Component({
  selector: 'app-audit-trail-page',
  imports: [CommonModule],
  templateUrl: './audit-trail-page.html',
  styleUrl: './audit-trail-page.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AuditTrailPage {
  private readonly layout = inject(LayoutService);
  private readonly service = inject(AuditTrailService);

  protected readonly logs = this.service.logs;
  protected readonly emptyMessage = this.service.emptyMessage;

  constructor() {
    this.layout.title.set('Auditoría');
  }
}
