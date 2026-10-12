import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { interval, Observable, startWith, switchMap } from 'rxjs';

import { environment } from '../../environments/environment';

export interface AssignmentEvent {
  id_evento: number;
  turno: string;
  mesa: number;
  mensaje: string;
}

export interface Desk {
  id: number;
  nombre: string;
  estado: 'disponible' | 'ocupada';
  turno_actual: string | null;
}

export interface AppState {
  ventanillas: Desk[];
  turnos_en_espera: string[];
  cantidad_espera: number;
  ultimo_llamado: AssignmentEvent | null;
  siguiente_turno: string;
  total_generados: number;
  total_atendidos: number;
}

export interface CreatedTurn {
  turno: string;
  estado: 'asignado' | 'en_espera';
  mesa: number | null;
  asignacion: AssignmentEvent | null;
}

export interface FinishDeskResponse {
  mesa: number;
  turno_finalizado: string | null;
}

export interface CallNextResponse {
  mesa: number;
  asignacion: AssignmentEvent;
}

@Injectable({ providedIn: 'root' })
export class TurnosService {
  private readonly apiUrl = environment.apiUrl;

  constructor(private readonly http: HttpClient) {}

  pollState(): Observable<AppState> {
    return interval(1000).pipe(
      startWith(0),
      switchMap(() => this.getState())
    );
  }

  getState(): Observable<AppState> {
    return this.http.get<AppState>(`${this.apiUrl}/estado`);
  }

  createTurn(): Observable<CreatedTurn> {
    return this.http.post<CreatedTurn>(`${this.apiUrl}/turnos`, {});
  }

  callNext(id: number): Observable<CallNextResponse> {
    return this.http.post<CallNextResponse>(`${this.apiUrl}/ventanillas/${id}/llamar`, {});
  }

  finishDesk(id: number): Observable<FinishDeskResponse> {
    return this.http.post<FinishDeskResponse>(`${this.apiUrl}/ventanillas/${id}/finalizar`, {});
  }
}

