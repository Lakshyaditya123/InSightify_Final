import { Component, Input, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Merged_idea_large, CurrUser, Comments, ApiResponse } from '../../services/api-interfaces';
import { AuthService } from '../../services/auth';
import { IdeaService } from '../../services/idea'; // Import IdeaService
import { CommentsClass } from '../../components/comments/comments';

@Component({
  selector: 'app-merged-idea-details',
  standalone: true,
  imports: [CommonModule, CommentsClass],
  templateUrl: './merged-idea-details.html',
  styleUrl: './merged-idea-details.css'  // Reusing your existing styles
})
export class MergedIdeaDetails {
  @Input() cardData!: Merged_idea_large;
  @Input() isCommentsVisible!: boolean;

  currentUserId:number=-1;
  all_comment_cards: Comments[] = [];
  constructor(private authService: AuthService, private ideaService: IdeaService) {}
  ngOnInit() {
      const currentUser: CurrUser | null = this.authService.getCurrentUser();
      if (currentUser) {
        this.currentUserId = currentUser.user_id;
        if (this.isCommentsVisible) {
        this.get_all_comments();
      }
      } else {
        console.error('User not logged in!');
      }
    }
   ngOnChanges(changes: SimpleChanges) {
    if (changes['isCommentsVisible'] && changes['isCommentsVisible'].currentValue === true) {
      this.get_all_comments();
    }
  }
  get_all_comments() {
    if (!this.cardData) return;
    this.ideaService.get_all_comments(this.currentUserId, null, this.cardData.merged_idea_details.id).subscribe({
      next: (res: ApiResponse) => {
        if (res.errCode === 0 && res.data?.all_comments) {
          this.all_comment_cards = res.data.all_comments;
        } else {
          this.all_comment_cards = [];
        }
      },
      error: (err) => {
        console.error("Error fetching comments:", err);
        this.all_comment_cards = [];
      }
    });
  }
  showAllTags = false;
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

  // Convert size to idea type label
  getIdeaTypeLabel(): string {
    return 'Human Idea';
  }

  // Get CSS class for idea type badge
  getIdeaTypeClass(): string {
    return 'bg-primary'; // Human ideas - blue
  }
}

