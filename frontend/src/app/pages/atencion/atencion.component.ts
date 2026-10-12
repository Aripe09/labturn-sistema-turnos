import { CommonModule } from '@angular/common';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Subscription } from 'rxjs';

import { AppState, Desk, TurnosService } from '../../core/turnos.service';
import { BrandComponent } from '../../shared-brand';

@Component({
  selector: 'app-atencion',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatIconModule, BrandComponent],
  templateUrl: './atencion.component.html',
  styleUrl: './atencion.component.scss'
})
export class AtencionComponent implements OnInit, OnDestroy {
  state: AppState | null = null;
  busyDeskId: number | null = null;
  private readonly subscriptions = new Subscription();

  constructor(
    private readonly turnosService: TurnosService,
    private readonly snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.subscriptions.add(
      this.turnosService.pollState().subscribe((state) => this.state = state)
    );
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
  }

  finalizar(desk: Desk): void {
    if (this.busyDeskId !== null || !desk.turno_actual) {
      return;
    }

    this.busyDeskId = desk.id;
    this.turnosService.finishDesk(desk.id).subscribe({
      next: (response) => {
        const message = response.nueva_asignacion
          ? `${response.nueva_asignacion.turno} asignado a Mesa ${response.nueva_asignacion.mesa}`
          : `Mesa ${desk.id} disponible`;
        this.snackBar.open(message, 'OK', { duration: 2400 });
        this.busyDeskId = null;
      },
      error: () => {
        this.snackBar.open('No se pudo finalizar la atencion', 'OK', { duration: 2600 });
        this.busyDeskId = null;
      }
    });
  }

  trackDesk(_: number, desk: Desk): number {
    return desk.id;
  }
}

