import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZoneChangeDetection } from '@angular/core';
import { CommonModule } from '@angular/common'; // 👈
import { provideRouter } from '@angular/router';
import { FormsModule } from '@angular/forms'; // 👈 Importer ici
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    // Ajoute FormsModule comme provider via ce hack temporaire
    { provide: 'ADD_STANDALONE_IMPORTS', useValue: () => [CommonModule, FormsModule] }
  ]
};
