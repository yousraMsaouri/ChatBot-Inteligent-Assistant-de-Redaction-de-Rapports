// src/app/chatbot/chatbot.component.ts
import { CommonModule } from '@angular/common';
import { Component, OnInit, AfterViewChecked, ViewChild, ElementRef } from '@angular/core';
import { FormsModule } from '@angular/forms';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css'],
  // ✅ Ajoute les imports ici (nouveau style standalone)
  imports: [
    CommonModule,     // Pour @if, @for
    FormsModule       // Pour [(ngModel)]
  ],
  standalone: true   // Très important
})
export class ChatbotComponent implements OnInit, AfterViewChecked {
  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;

  messages: Message[] = [
    { sender: 'bot', text: 'Bonjour ! Je suis votre assistant pour la rédaction de rapports. Comment puis-je vous aider ?' }
  ];
  userInput = '';

  ngOnInit(): void {
    // Chargement initial
  }

  ngAfterViewChecked(): void {
    // Défilement automatique vers le bas
    this.scrollToBottom();
  }

  scrollToBottom(): void {
    try {
      this.messagesContainer.nativeElement.scrollTop =
        this.messagesContainer.nativeElement.scrollHeight;
    } catch (err) {}
  }

  async sendMessage(): Promise<void> {
    if (!this.userInput.trim()) return;

    // Ajouter le message utilisateur
    this.messages.push({ sender: 'user', text: this.userInput });

    // Nettoyer le champ
    const userMessage = this.userInput;
    this.userInput = '';

    // Appeler l'API FastAPI
    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_id: 'user_123',
          message: userMessage
        })
      });

      const data = await response.json();
      this.messages.push({ sender: 'bot', text: data.response });
    } catch (error) {
      this.messages.push({
        sender: 'bot',
        text: 'Désolé, je ne peux pas me connecter au serveur. Vérifiez que FastAPI est lancé.'
      });
    }
  }

  // Permet d'envoyer avec la touche Entrée
  onKeyEnter(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }
}