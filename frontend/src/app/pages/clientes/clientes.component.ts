import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
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
        error: (error: HttpErrorResponse) => {
          this.error = this.describeHttpError(error, 'No se pudo consultar el estado del sistema.');
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
          this.detalle = 'Tu turno esta en espera';
        },
        error: (error: HttpErrorResponse) => {
          this.error = this.describeHttpError(error, 'No fue posible generar el turno. Intentalo nuevamente.');
        }
      });
  }

  private describeHttpError(error: HttpErrorResponse, fallback: string): string {
    const serverMessage = error.error?.mensaje || error.error?.error;
    if (serverMessage) {
      return serverMessage;
    }

    if (error.status === 0) {
      return 'No se pudo conectar con el servidor. Revisa tu conexion e intentalo de nuevo.';
    }

    return fallback;
  }
}

