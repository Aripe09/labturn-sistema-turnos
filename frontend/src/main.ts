import { provideHttpClient } from '@angular/common/http';
import { enableProdMode, importProvidersFrom } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideRouter, Routes } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBarModule } from '@angular/material/snack-bar';

import { AppComponent } from './app/app.component';
import { environment } from './environments/environment';
import { ClientesComponent } from './app/pages/clientes/clientes.component';
import { MonitorComponent } from './app/pages/monitor/monitor.component';
import { AtencionComponent } from './app/pages/atencion/atencion.component';

if (environment.production) {
  enableProdMode();
}

const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'clientes' },
  { path: 'clientes', component: ClientesComponent },
  { path: 'clientes/monitor', component: MonitorComponent },
  { path: 'atencion', component: AtencionComponent },
  { path: '**', redirectTo: 'clientes' }
];

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes),
    provideHttpClient(),
    provideAnimations(),
    importProvidersFrom(
      MatButtonModule,
      MatCardModule,
      MatIconModule,
      MatProgressSpinnerModule,
      MatSnackBarModule
    )
  ]
}).catch((error) => console.error(error));

