import { Component, ViewChild, ElementRef, Input, OnInit, OnChanges, SimpleChanges } from '@angular/core';
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
  @Input() isIdeaCommentsVisible!: boolean;

  @ViewChild('scrollToComments') scrollToComments!: ElementRef;

  currentUserId: number = -1;
  all_comment: Comments[] = [];

  constructor(private authService: AuthService, private ideaService: IdeaService) {}

  ngOnInit() {
    const currentUser: CurrUser | null = this.authService.getCurrentUser();
    if (currentUser) {
      this.currentUserId = currentUser.user_id;
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['isIdeaCommentsVisible']) {
      const commentsVisibleChange = changes['isIdeaCommentsVisible'];
        // if (commentsVisibleChange.currentValue === true && this.all_comment.length === 0) {
        //   console.log("On changes get all comments triggered");
        //     this.get_all_comments();
        // }
        // Clear comments when the section is hidden
        // if (commentsVisibleChange.currentValue === false && commentsVisibleChange.previousValue === true) {
        //     this.all_comment = [];
        // }
        if (commentsVisibleChange.currentValue === true) {
            this.get_all_comments();
            setTimeout(() => this.scrollToCommentSection(), 500);
        }
    }
  }

  private scrollToCommentSection() {
    if (this.scrollToComments?.nativeElement) {
      this.scrollToComments.nativeElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
  
  get_all_comments() {
    if (!this.cardData) return;
    this.ideaService.get_all_comments(this.currentUserId, this.cardData.idea_details.id, null).subscribe({
      next: (res: ApiResponse) => {
        this.all_comment = res.data || [];
        console.log("Comments for single idea fetched:", this.all_comment);
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
  getStatusTitle(status:number){
  switch(status){
    case -1: return 'Idea Declined';
    case 0: return 'Awating Approval';
    case 1: return 'Idea Approved';
    default: return 'Status Unknown'; // fallback
  }
}
}