import { CommonModule } from '@angular/common';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Observable, Subscription } from 'rxjs';

import { AppState, AssignmentEvent, Desk, TurnosService } from '../../core/turnos.service';
import { SoundService } from '../../core/sound.service';
import { BrandComponent } from '../../shared-brand';

@Component({
  selector: 'app-monitor',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatIconModule, BrandComponent],
  templateUrl: './monitor.component.html',
  styleUrl: './monitor.component.scss'
})
export class MonitorComponent implements OnInit, OnDestroy {
  state: AppState | null = null;
  now = new Date();
  announcement: AssignmentEvent | null = null;
  private readonly subscriptions = new Subscription();
  private lastEventId: number | null = null;
  private hideTimer: ReturnType<typeof setTimeout> | null = null;

  constructor(
    private readonly turnosService: TurnosService,
    public readonly soundService: SoundService
  ) {}

  ngOnInit(): void {
    this.subscriptions.add(
      this.turnosService.pollState().subscribe((state) => {
        this.state = state;
        this.handleEvent(state.ultimo_llamado);
      })
    );

    this.subscriptions.add(
      new ObservableClock().tick().subscribe((date) => this.now = date)
    );
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
    if (this.hideTimer) {
      clearTimeout(this.hideTimer);
    }
  }

  activarSonido(): void {
    void this.soundService.enable();
  }

  trackDesk(_: number, desk: Desk): number {
    return desk.id;
  }

  private handleEvent(event: AssignmentEvent | null): void {
    if (!event || event.id_evento === this.lastEventId) {
      return;
    }

    this.lastEventId = event.id_evento;
    this.announcement = event;
    this.soundService.playBell();

    if (this.hideTimer) {
      clearTimeout(this.hideTimer);
    }

    this.hideTimer = setTimeout(() => {
      this.announcement = null;
    }, 5200);
  }
}

class ObservableClock {
  tick() {
    return new Observable<Date>((subscriber) => {
      subscriber.next(new Date());
      const timer = setInterval(() => subscriber.next(new Date()), 1000);
      return () => clearInterval(timer);
    });
  }
}

