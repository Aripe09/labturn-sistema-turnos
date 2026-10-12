import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class SoundService {
  private context: AudioContext | null = null;
  private enabled = false;

  get isEnabled(): boolean {
    return this.enabled;
  }

  async enable(): Promise<void> {
    this.context = this.context ?? new AudioContext();
    await this.context.resume();
    this.enabled = true;
    this.playBell();
  }

  playBell(): void {
    if (!this.enabled || !this.context) {
      return;
    }

    const now = this.context.currentTime;
    this.tone(880, now, 0.09, 0.035);
    this.tone(1320, now + 0.08, 0.12, 0.03);
  }

  private tone(frequency: number, start: number, duration: number, gain: number): void {
    if (!this.context) {
      return;
    }

    const oscillator = this.context.createOscillator();
    const envelope = this.context.createGain();
    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(frequency, start);
    envelope.gain.setValueAtTime(0.0001, start);
    envelope.gain.exponentialRampToValueAtTime(gain, start + 0.015);
    envelope.gain.exponentialRampToValueAtTime(0.0001, start + duration);
    oscillator.connect(envelope);
    envelope.connect(this.context.destination);
    oscillator.start(start);
    oscillator.stop(start + duration + 0.02);
  }
}

