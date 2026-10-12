import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class SoundService {
  private context: AudioContext | null = null;
  private enabled = false;
  private masterGain: GainNode | null = null;

  get isEnabled(): boolean {
    return this.enabled;
  }

  async enable(): Promise<void> {
    this.context = this.context ?? new AudioContext();
    this.masterGain = this.masterGain ?? this.context.createGain();
    this.masterGain.gain.value = 0.18;
    this.masterGain.connect(this.context.destination);
    await this.context.resume();
    this.enabled = true;
    this.playBell();
  }

  disable(): void {
    this.enabled = false;
  }

  async toggle(): Promise<void> {
    if (this.enabled) {
      this.disable();
      return;
    }

    await this.enable();
  }

  playBell(): void {
    if (!this.enabled || !this.context || !this.masterGain) {
      return;
    }

    const now = this.context.currentTime;
    this.tone(740, now, 0.42, 0.08);
    this.tone(988, now + 0.16, 0.55, 0.055);
    this.tone(1480, now + 0.32, 0.34, 0.025);
  }

  private tone(frequency: number, start: number, duration: number, gain: number): void {
    if (!this.context || !this.masterGain) {
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
    envelope.connect(this.masterGain);
    oscillator.start(start);
    oscillator.stop(start + duration + 0.02);
  }
}

