import { Component, Input, Output, OnInit, OnChanges, EventEmitter, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiResponse, Comments, AddComment } from '../../services/api-interfaces';
import { IdeaService } from '../../services/idea';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-comments',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './comments.html',
  styleUrls: ['./comments.css']
})
export class CommentsClass implements OnInit, OnChanges {
  @Input() all_comment: Comments[] = [];
  @Input() card!: any; // This can be Idea_large or Merged_idea_large
  @Input() currentUserId!: number;
  @Output() commentPosted = new EventEmitter<void>();

  newCommentText = '';

  constructor(private ideaService: IdeaService) {}

  ngOnInit() {
    this.addUiStateToComments();
  }
  
  // When the input comment list changes, re-apply the UI state properties.
  ngOnChanges(changes: SimpleChanges) {
    if (changes['all_comment']) {
      this.addUiStateToComments();
    }
  }

  // Add properties needed for the UI (like reply form state) to each comment object.
  private addUiStateToComments() {
    if (this.all_comment) {
      this.all_comment.forEach(comment => {
        comment.replying = false;
        comment.newReplyText = '';
        if (comment.replies) {
          comment.replies.forEach(reply => {
            reply.replying = false; // Not used, but good for consistency
            reply.newReplyText = '';
          });
        }
      });
    }
  }

  postNewComment() {
    if (!this.newCommentText.trim()) return;

    const isMerged = 'merged_idea_details' in this.card;
    const ideaId = isMerged ? this.card.merged_idea_details.id : this.card.idea_details.id;

    const newCommentPayload: AddComment = {
      user_id: this.currentUserId,
      idea_id: isMerged ? null : ideaId,
      merged_idea_id: isMerged ? ideaId : null,
      content: this.newCommentText.trim(),
      parent_comment: -1 // Top-level comment
    };

    this.ideaService.addComment(newCommentPayload).subscribe({
      next: (res: ApiResponse) => {
        if (res.errCode === 0) {
          this.newCommentText = '';
          this.commentPosted.emit(); // Notify parent to refresh comments
        } else {
          console.error("Failed to add comment:", res.message);
        }
      },
      error: (err) => console.error("Error adding comment:", err)
    });
  }

  async toggleLike(comment: Comments) {
    const originalVote = comment.user_vote;
    const originalLikes = comment.likes;

    // Optimistically update UI
    comment.user_vote = (comment.user_vote === 1) ? 0 : 1;
    comment.likes += (comment.user_vote === 1) ? 1 : -1;

    const payload = { 
      comment_id: comment.comment_id, 
      user_id: this.currentUserId, 
      vote_type: comment.user_vote 
    };

    try {    
      const result: ApiResponse = await firstValueFrom(this.ideaService.updateVote(payload));
      if (result.errCode !== 0) {
        // Revert UI on error
        comment.user_vote = originalVote;
        comment.likes = originalLikes;
        console.error("Failed to update vote:", result.message);
      }
    } catch (error) {
      // Revert UI on error
      comment.user_vote = originalVote;
      comment.likes = originalLikes;
      console.error('Error liking comment:', error);
    }
  }

  toggleReplyForm(comment: Comments) {
    const isCurrentlyReplying = comment.replying;
    // Close all other forms
    this.all_comment.forEach(c => c.replying = false);
    // Toggle the selected one
    comment.replying = !isCurrentlyReplying;
  }

  postReply(parentComment: Comments) {
    const replyText = parentComment.newReplyText?.trim();
    if (!replyText) return;

    const isMerged = 'merged_idea_details' in this.card;
    const ideaId = isMerged ? this.card.merged_idea_details.id : this.card.idea_details.id;
    
    const replyPayload: AddComment = {
      user_id: this.currentUserId,
      idea_id: isMerged ? null : ideaId,
      merged_idea_id: isMerged ? ideaId : null,
      content: replyText,
      parent_comment: parentComment.comment_id
    };

    this.ideaService.addComment(replyPayload).subscribe({
      next: (res: ApiResponse) => {
        if (res.errCode === 0) {
          parentComment.replying = false;
          parentComment.newReplyText = '';
          this.commentPosted.emit(); // Notify parent to refresh
        } else {
          console.error("Failed to add reply:", res.message);
        }
      },
      error: (err) => console.error("Error adding reply:", err)
    });
  }
}
