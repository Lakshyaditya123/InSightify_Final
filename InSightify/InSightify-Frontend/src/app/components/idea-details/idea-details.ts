import {Component, Input} from '@angular/core';
import {CommonModule} from '@angular/common';

@Component({
  selector: 'app-idea-details',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './idea-details.html',
  styleUrl: './idea-details.css'
})
export class IdeaDetails {
  @Input() cardData: any;

  // Convert size to idea type label
  getIdeaTypeLabel(size: string): string {
    switch (size.toLowerCase()) {
      case 'small':
        return 'Human Idea';
      case 'medium':
        return 'AI Merged';
      case 'large':
        return 'AI Enhanced';
      default:
        return 'Human Idea';
    }
  }

  // Get CSS class for idea type badge
  getIdeaTypeClass(size: string): string {
    switch (size.toLowerCase()) {
      case 'small':
        return 'bg-primary'; // Human ideas - blue
      case 'medium':
        return 'bg-warning text-dark'; // AI merged - yellow/orange
      case 'large':
        return 'bg-success'; // AI enhanced - green
      default:
        return 'bg-primary';
    }
  }
}
