import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { finalize } from 'rxjs';

import { TurnosService } from '../../core/turnos.service';
import { BrandComponent } from '../../shared-brand';

@Component({
  selector: 'app-clientes',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatIconModule, BrandComponent],
  templateUrl: './clientes.component.html',
  styleUrl: './clientes.component.scss'
})
export class ClientesComponent {
  turno: string | null = null;
  detalle: string | null = null;
  loading = false;

  constructor(private readonly turnosService: TurnosService) {}

  generarTurno(): void {
    if (this.loading) {
      return;
    }

    this.loading = true;
    this.turnosService.createTurn()
      .pipe(finalize(() => this.loading = false))
      .subscribe({
        next: (response) => {
          this.turno = response.turno;
          this.detalle = response.estado === 'asignado' && response.mesa
            ? `Pasa a Mesa ${response.mesa.mesa}`
            : 'Tu turno esta en espera';
        }
      });
  }
}

