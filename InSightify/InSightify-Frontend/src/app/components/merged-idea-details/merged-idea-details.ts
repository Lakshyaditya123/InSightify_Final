import { Component, Input, Output, EventEmitter} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Idea_large, CurrUser } from '../../services/api-interfaces';
import { Merged_idea_large,  } from '../../services/api-interfaces';
import { Comment } from '../comments/comments';
import { AuthService } from '../../services/auth';
import { VotesSection } from '../../components/votes-section/votes-section';

@Component({
  selector: 'app-merged-idea-details',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './merged-idea-details.html',
  styleUrl: './merged-idea-details.css'  // Reusing your existing styles
})
export class MergedIdeaDetails {
  @Input() cardData!: Merged_idea_large;
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

    showAllTags = false;
  commentsVisible = false;
  maxVisibleTags = 4;

  get visibleTags() {
    if (!this.cardData?.merged_idea_details.tags_list) return [];
    return this.showAllTags 
      ? this.cardData.merged_idea_details.tags_list 
      : this.cardData.merged_idea_details.tags_list.slice(0, this.maxVisibleTags);
  }

   get hiddenTagsCount() {
    if (!this.cardData?.merged_idea_details.tags_list) return 0;
    return Math.max(0, this.cardData.merged_idea_details.tags_list.length - this.maxVisibleTags);
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
