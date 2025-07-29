// import { Component, ViewChild, ElementRef, Input, OnInit, OnChanges, SimpleChanges} from '@angular/core';
// import { CommonModule } from '@angular/common';
// import { Merged_idea_large, CurrUser, Comments, ApiResponse } from '../../services/api-interfaces';
// import { AuthService } from '../../services/auth';
// import { IdeaService } from '../../services/idea';
// import { CommentsClass } from '../../components/comments/comments';

// @Component({
//   selector: 'app-merged-idea-details',
//   standalone: true,
//   imports: [CommonModule, CommentsClass],
//   templateUrl: './merged-idea-details.html',
//   styleUrl: './merged-idea-details.css'
// })
// export class MergedIdeaDetails implements OnInit, OnChanges {
//   @Input() cardData!: Merged_idea_large;
//   @Input() isCommentsVisible!: boolean;

//   @ViewChild('scrollToComments') scrollToComments!: ElementRef;

//   currentUserId: number = -1;
//   all_comment_cards: Comments[] = [];

//   constructor(private authService: AuthService, private ideaService: IdeaService) {}

//   ngOnInit() {
//     const currentUser: CurrUser | null = this.authService.getCurrentUser();
//     if (currentUser) {
//       this.currentUserId = currentUser.user_id;
//     } else {
//       console.error('User not logged in!');
//     }
//   }

//   ngOnChanges(changes: SimpleChanges) {
//     if (changes['isCommentsVisible'] && changes['isCommentsVisible'].currentValue === true) {
//       this.get_all_comments();
//       setTimeout(() => this.scrollToCommentSection(), 500);
//     }
//   }

//   private scrollToCommentSection() {
//     if (this.scrollToComments?.nativeElement) {
//       this.scrollToComments.nativeElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
//     }
//   }
  
//   get_all_comments() {
//     if (!this.cardData) return;
//     this.ideaService.get_all_comments(this.currentUserId, null, this.cardData.merged_idea_details.id).subscribe({
//       next: (res: ApiResponse) => {
//         this.all_comment_cards = res.data || [];
//       },
//       error: (err) => {
//         console.error("Error fetching comments:", err);
//         this.all_comment_cards = [];
//       }
//     });
//     console.log("comments: ", this.all_comment_cards)
//   }
// }

import { Component, ViewChild, ElementRef, Input, OnInit, OnChanges, SimpleChanges, ChangeDetectorRef } from '@angular/core';
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
  @Input() isMergedCommentsVisible!: boolean;
  @ViewChild('scrollToComments') scrollToComments!: ElementRef;

  currentUserId: number = -1;
  all_comment: Comments[] = [];

  constructor(
    private authService: AuthService, 
    private ideaService: IdeaService,
    private cdr: ChangeDetectorRef // Inject ChangeDetectorRef
  ) {}

  ngOnInit() {
    const currentUser: CurrUser | null = this.authService.getCurrentUser();
    if (currentUser) {
      this.currentUserId = currentUser.user_id;
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['isMergedCommentsVisible']) {
        const commentsVisibleChange = changes['isMergedCommentsVisible'];
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
    this.ideaService.get_all_comments(this.currentUserId, null, this.cardData.merged_idea_details.id).subscribe({
      next: (res: ApiResponse) => {
        this.all_comment = res.data || [];
        console.log("Comments for merged idea fetched:", this.all_comment);
        this.cdr.detectChanges(); // Manually trigger change detection
      },
      error: (err) => {
        console.error("Error fetching comments:", err);
        this.all_comment = [];
      }
    });
  }
}