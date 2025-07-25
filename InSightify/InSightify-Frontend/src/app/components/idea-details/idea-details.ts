import {Component, Input, OnChanges, OnInit, SimpleChanges} from '@angular/core';
import {CommonModule} from '@angular/common';
import { Idea_large, CurrUser, Comments, ApiResponse} from '../../services/api-interfaces';
import { AuthService } from '../../services/auth';
import { IdeaService } from '../../services/idea';
import { CommentsClass } from '../../components/comments/comments';


@Component({
  selector: 'app-idea-details',
  standalone: true,
  imports: [CommonModule,CommentsClass],
  templateUrl: './idea-details.html',
  styleUrl: './idea-details.css'
})
export class IdeaDetails implements OnInit, OnChanges {
  @Input() cardData!: Idea_large;
  @Input() mySpace!: boolean;
  @Input() isCommentsVisible!: boolean;
  @Input() modalwidth!: number;
  // This will hold the current user's ID, which is used to check if the user is logged in.
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
    if (!this.cardData) return; // Guard clause
    this.ideaService.get_all_comments(this.currentUserId, this.cardData.idea_details.id).subscribe({
      next: (res: ApiResponse) => {
        if (res.errCode === 0 && res.data?.all_comments) {
          this.all_comment_cards = res.data.all_comments;
        } else {
          this.all_comment_cards = []; // Ensure it's an empty array on error or no data
        }
      },
      error: (err) => {
        console.error("Error fetching comments:", err);
        this.all_comment_cards = [];
      }
    });
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
  showMoreTags() {
    this.showAllTags = true;
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

