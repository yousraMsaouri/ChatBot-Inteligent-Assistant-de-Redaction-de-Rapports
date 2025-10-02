import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Chatbot } from './chatbot.component';

describe('Chatbot', () => {
  let component: Chatbot;
  let fixture: ComponentFixture<Chatbot>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Chatbot]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Chatbot);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
