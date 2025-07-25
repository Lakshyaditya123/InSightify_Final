import { Component, ViewChild, ElementRef, Input, OnInit, OnChanges, SimpleChanges, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Idea_large, CurrUser, Comments, ApiResponse } from '../../services/api-interfaces';
import { AuthService } from '../../services/auth';
import { IdeaService } from '../../services/idea';
import { CommentsClass } from '../../components/comments/comments';

@Component({
  selector: 'app-idea-details',
  standalone: true,
  imports: [CommonModule, CommentsClass],
  templateUrl: './idea-details.html',
  styleUrl: './idea-details.css'
})
export class IdeaDetails implements OnInit, OnChanges {
  @Input() cardData!: Idea_large;
  @Input() mySpace!: boolean;
  @Input() isCommentsVisible!: boolean;

  @ViewChild('scrollToComments') scrollToComments!: ElementRef;

  currentUserId: number = -1;
  all_comment: Comments[] = [];

  constructor(private authService: AuthService, private ideaService: IdeaService) {}

  ngOnInit() {
    const currentUser: CurrUser | null = this.authService.getCurrentUser();
    console.log("this.isCommentsVisible, oninit", this.isCommentsVisible)
    if (currentUser) {
      this.currentUserId = currentUser.user_id;
    } else {
      console.error('User not logged in!');
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    console.log("this.isCommentsVisible onchanges before", this.isCommentsVisible)
    // This is the only place we need to handle the scrolling logic.
    if (changes['isCommentsVisible'] && changes['isCommentsVisible'].currentValue === true) {
      this.get_all_comments();
      console.log(this.all_comment)

      // Use setTimeout to wait for the view to render, then scroll smoothly.
      setTimeout(() => this.scrollToCommentSection(), 500); // 150ms is a safe delay.
      console.log("this.isCommentsVisible onchanges after", this.isCommentsVisible)
    }
  }



  private scrollToCommentSection() {
    if (this.scrollToComments?.nativeElement) {
      this.scrollToComments.nativeElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
  
  get_all_comments() {
    if (!this.cardData) return;
    this.ideaService.get_all_comments(this.currentUserId, this.cardData.idea_details.id).subscribe({
      next: (res: ApiResponse) => {
        this.all_comment = res.data || [];
      },
      error: (err) => {
        console.error("Error fetching comments:", err);
        this.all_comment = [];
      }
    });
  }
  
  
  getStatusColor(status: number): string {
    switch (status) {
      case -1: return 'red';
      case 0: return 'gray';
      case 1: return 'green';
      default: return 'gray';
    }
  }
}