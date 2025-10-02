import { Component, signal } from '@angular/core';
import { ChatbotComponent } from './chatbot/chatbot.component'; // ✅ Importe le composant


@Component({
  selector: 'app-root',
  imports: [ChatbotComponent ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  protected readonly title = signal('frontend-chatbot');
}
