import { Component, ViewChild, ElementRef, Input, OnInit, OnChanges, SimpleChanges, OnDestroy} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Merged_idea_large, CurrUser, Comments, ApiResponse } from '../../services/api-interfaces';
import { AuthService } from '../../services/auth';
import { IdeaService } from '../../services/idea';
import { CommentsClass } from '../../components/comments/comments';

@Component({
  selector: 'app-merged-idea-details',
  standalone: true,
  imports: [CommonModule, CommentsClass],
  templateUrl: './merged-idea-details.html',
  styleUrl: './merged-idea-details.css'
})
export class MergedIdeaDetails implements OnInit, OnChanges {
  @Input() cardData!: Merged_idea_large;
  @Input() isCommentsVisible!: boolean;

  @ViewChild('scrollToComments') scrollToComments!: ElementRef;

  currentUserId: number = -1;
  all_comment_cards: Comments[] = [];

  constructor(private authService: AuthService, private ideaService: IdeaService) {}

  ngOnInit() {
    const currentUser: CurrUser | null = this.authService.getCurrentUser();
    if (currentUser) {
      this.currentUserId = currentUser.user_id;
    } else {
      console.error('User not logged in!');
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    // This logic now matches the other component exactly.
    if (changes['isCommentsVisible'] && changes['isCommentsVisible'].currentValue === true) {
      this.get_all_comments();
      // Wait for the view to render, then scroll smoothly.
      setTimeout(() => this.scrollToCommentSection(), 500);
    }
  }

  private scrollToCommentSection() {
    if (this.scrollToComments?.nativeElement) {
      this.scrollToComments.nativeElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
  
  get_all_comments() {
    if (!this.cardData) return;
    this.ideaService.get_all_comments(this.currentUserId, null, this.cardData.merged_idea_details.id).subscribe({
      next: (res: ApiResponse) => {
        this.all_comment_cards = res.data || [];
      },
      error: (err) => {
        console.error("Error fetching comments:", err);
        this.all_comment_cards = [];
      }
    });
  }
}