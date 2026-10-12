import { Component, Input } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-brand',
  standalone: true,
  imports: [MatIconModule],
  template: `
    <div class="brand" [class.brand--light]="light">
      <div class="brand__mark">
        <mat-icon>science</mat-icon>
      </div>
      <div>
        <strong>LabTurn</strong>
        <span>Sistema Inteligente de Turnos</span>
      </div>
    </div>
  `
})
export class BrandComponent {
  @Input() light = false;
}

