import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Subscription, finalize } from 'rxjs';

import { AppState, TurnosService } from '../../core/turnos.service';
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
  error: string | null = null;
  state: AppState | null = null;
  loading = false;
  private readonly subscriptions = new Subscription();

  constructor(private readonly turnosService: TurnosService) {}

  ngOnInit(): void {
    this.subscriptions.add(
      this.turnosService.pollState().subscribe({
        next: (state) => {
          this.state = state;
          this.error = null;
        },
        error: () => {
          this.error = 'No se pudo conectar con el backend Flask. Verifica que este ejecutandose en http://127.0.0.1:5000.';
        }
      })
    );
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
  }

  generarTurno(): void {
    if (this.loading) {
      return;
    }

    this.loading = true;
    this.error = null;
    this.turnosService.createTurn()
      .pipe(finalize(() => this.loading = false))
      .subscribe({
        next: (response) => {
          this.turno = response.turno;
          this.detalle = response.estado === 'asignado' && response.mesa !== null
            ? `Pasa a Mesa ${response.mesa}`
            : 'Tu turno esta en espera';
        },
        error: () => {
          this.error = 'No fue posible generar el turno. Confirma que Flask este activo y vuelve a intentarlo.';
        }
      });
  }
}

