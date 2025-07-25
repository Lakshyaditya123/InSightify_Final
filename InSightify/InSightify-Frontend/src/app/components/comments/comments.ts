import { Component, Input, Output, OnChanges, EventEmitter, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiResponse, Comments, AddComment, Idea_large, Merged_idea_large } from '../../services/api-interfaces';
import { IdeaService } from '../../services/idea';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-comments',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './comments.html',
  styleUrls: ['./comments.css']
})
export class CommentsClass implements OnChanges {
  // These inputs are passed down from the parent component (idea-details or merged-idea-details).
  @Input() all_comment: Comments[] = [];
  @Input() card!: Idea_large | Merged_idea_large;
  @Input() currentUserId!: number;
  @Output() commentPosted = new EventEmitter<void>();
  // This is our internal list that holds the comments with UI-specific properties.
  // The template will always read from this list.
  processed_comments: Comments[] = [];
  newCommentText = '';

  constructor(private ideaService: IdeaService) {}

  // This is the correct lifecycle hook to detect when the parent passes a new list of comments.
  ngOnChanges(changes: SimpleChanges) {
    console.log(this.all_comment)
    if (changes['all_comment']) {
      this.processIncomingComments();
    }
  }

  /**
   * This is the key function. It takes the raw comment list from the parent's @Input()
   * and maps it to our internal 'processed_comments' array, adding the necessary
   * properties for the UI to function correctly (like 'replying' state).
   */
  private processIncomingComments() {
    if (this.all_comment && Array.isArray(this.all_comment)) {
      this.processed_comments = this.all_comment.map(comment => ({
        ...comment,
        replying: false,
        newReplyText: '',
        replies: comment.replies ? comment.replies.map(reply => ({...reply})) : [] // Ensure replies are also processed
      }));
    } else {
      this.processed_comments = [];
    }
  }

  /**
   * Safely determines the correct idea_id or merged_idea_id from the card input.
   * This uses a type guard to satisfy TypeScript.
   */
  private getIdeaIdentifiers(): { ideaId: number | null, mergedIdeaId: number | null } {
    if ('merged_idea_details' in this.card) {
      return { ideaId: null, mergedIdeaId: this.card.merged_idea_details.id };
    } else {
      return { ideaId: this.card.idea_details.id, mergedIdeaId: null };
    }
  }

  postNewComment() {
    if (!this.newCommentText.trim()) return;

    const { ideaId, mergedIdeaId } = this.getIdeaIdentifiers();

    const newCommentPayload: AddComment = {
      user_id: this.currentUserId,
      idea_id: ideaId,
      merged_idea_id: mergedIdeaId,
      content: this.newCommentText.trim(),
      parent_comment: null
    };

    this.ideaService.addComment(newCommentPayload).subscribe({
      next: (res: ApiResponse) => {
        if (res.errCode === 0) {
          this.newCommentText = '';
          this.commentPosted.emit(); // Notify parent to refresh the comments list
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

    // Optimistically update the UI for a responsive feel
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
        // If the API call fails, revert the UI to its original state
        comment.user_vote = originalVote;
        comment.likes = originalLikes;
        console.error("Failed to update vote:", result.message);
      }
    } catch (error) {
      comment.user_vote = originalVote;
      comment.likes = originalLikes;
      console.error('Error liking comment:', error);
    }
  }

  toggleReplyForm(comment: Comments) {
    const isCurrentlyReplying = comment.replying;
    // Close all other reply forms
    this.processed_comments.forEach(c => { c.replying = false; });
    // Toggle the selected one
    comment.replying = !isCurrentlyReplying;
  }

  postReply(parentComment: Comments) {
    const replyText = parentComment.newReplyText?.trim();
    if (!replyText) return;

    const { ideaId, mergedIdeaId } = this.getIdeaIdentifiers();

    const replyPayload: AddComment = {
      user_id: this.currentUserId,
      idea_id: ideaId,
      merged_idea_id: mergedIdeaId,
      content: replyText,
      parent_comment: parentComment.comment_id
    };

    this.ideaService.addComment(replyPayload).subscribe({
      next: (res: ApiResponse) => {
        if (res.errCode === 0) {
          this.commentPosted.emit(); // Notify parent to refresh all comments
        } else {
          console.error("Failed to add reply:", res.message);
        }
      },
      error: (err) => console.error("Error adding reply:", err)
    });
  }
}
