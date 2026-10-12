import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';

import { BrandComponent } from './shared-brand';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive, MatIconModule, BrandComponent],
  template: `
    <div class="app-shell">
      <aside class="app-nav">
        <app-brand />
        <nav aria-label="Navegacion principal">
          <a routerLink="/clientes" routerLinkActive="active">
            <mat-icon>confirmation_number</mat-icon>
            Generar turno
          </a>
          <a routerLink="/clientes/monitor" routerLinkActive="active">
            <mat-icon>monitor</mat-icon>
            Monitor de turnos
          </a>
          <a routerLink="/atencion" routerLinkActive="active">
            <mat-icon>support_agent</mat-icon>
            Mesas de atencion
          </a>
        </nav>
      </aside>
      <section class="app-content">
        <router-outlet />
      </section>
    </div>
  `
})
export class AppComponent {}

