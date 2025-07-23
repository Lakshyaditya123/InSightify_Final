import {Component, Input, Output, EventEmitter} from '@angular/core';
import {CommonModule} from '@angular/common';
import { Idea_large, CurrUser } from '../../services/api-interfaces';
import { Comment } from '../comments/comments';
import { AuthService } from '../../services/auth';
import { VotesSection } from '../../components/votes-section/votes-section';

@Component({
  selector: 'app-idea-details',
  standalone: true,
  imports: [CommonModule, VotesSection],
  templateUrl: './idea-details.html',
  styleUrl: './idea-details.css'
})
export class IdeaDetails {
  @Input() cardData!: Idea_large;
  @Input() mySpace!: boolean;
  @Output() closeModal = new EventEmitter<void>();
  currentUserId:number=-1;

  constructor(private authService: AuthService) {}
  ngOnInit() {
      const currentUser: CurrUser | null = this.authService.getCurrentUser();
      if (currentUser) {
        this.currentUserId = currentUser.user_id;
      } else {
        console.error('User not logged in!');
      }
    }
  getStatusColor(status: number): string {
  switch (status) {
    case -1: return 'red';
    case 0: return 'gray';
    case 1: return 'green';
    default: return 'gray'; // fallback
  }
}
  showAllTags = false;
  commentsVisible = false;
  maxVisibleTags = 4;

  get visibleTags() {
    if (!this.cardData?.idea_details?.tags_list) return [];
    return this.showAllTags 
      ? this.cardData.idea_details.tags_list 
      : this.cardData.idea_details.tags_list.slice(0, this.maxVisibleTags);
  }

   get hiddenTagsCount() {
    if (!this.cardData?.idea_details?.tags_list) return 0;
    return Math.max(0, this.cardData.idea_details.tags_list.length - this.maxVisibleTags);
  }

  get shouldShowMoreButton() {
    return !this.showAllTags && this.hiddenTagsCount > 0;
  }

   onClose() {
    this.closeModal.emit();
  }
  
  // Convert size to idea type label
  getIdeaTypeLabel(): string {
    return 'Human Idea';
  }

  // Get CSS class for idea type badge
  getIdeaTypeClass(): string {
    return 'bg-primary'; // Human ideas - blue
  }
}

