import { Component, Input } from '@angular/core';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import { CommonModule} from '@angular/common';

export interface Comment {
  id: number;
  author: string;
  content: string;
  parentId?: number | null;
}

@Component({
  selector: 'app-comments',
  templateUrl: './comments.html',
  imports: [
    ReactiveFormsModule,
    CommonModule
  ],
  styleUrl: './comments.css'
})
export class Comments {
  @Input() comments: Comment[] = [];
  @Input() ideaTitle: string = '';
  commentForm: FormGroup;
  replyForms: { [key: number]: FormGroup } = {};
  replyingTo: number | null = null;
  isSubmitting = false;

  constructor(private fb: FormBuilder) {
    this.commentForm = this.fb.group({
      content: ['', [Validators.required]]
    });
  }

  get topLevelComments(): Comment[] {
    return this.comments.filter(c => !c.parentId);
  }

  getReplies(parentId: number): Comment[] {
    return this.comments.filter(c => c.parentId === parentId);
  }

  startReply(commentId: number) {
    this.replyingTo = commentId;
    if (!this.replyForms[commentId]) {
      this.replyForms[commentId] = this.fb.group({
        content: ['', [Validators.required]]
      });
    }
  }

  cancelReply() {
    this.replyingTo = null;
  }

  submitComment() {
    if (this.commentForm.valid) {
      this.isSubmitting = true;
      const newComment: Comment = {
        id: Date.now(),
        author: 'Current User', // Replace with actual user
        content: this.commentForm.value.content,
        parentId: null
      };
      setTimeout(() => {
        this.comments.push(newComment);
        this.commentForm.reset();
        this.isSubmitting = false;
      }, 500);
    } else {
      this.commentForm.markAllAsTouched();
    }
  }

  submitReply(parentId: number) {
    const form = this.replyForms[parentId];
    if (form && form.valid) {
      const newReply: Comment = {
        id: Date.now(),
        author: 'Current User', // Replace with actual user
        content: form.value.content,
        parentId
      };
      setTimeout(() => {
        this.comments.push(newReply);
        form.reset();
        this.replyingTo = null;
      }, 500);
    } else if (form) {
      form.markAllAsTouched();
    }
  }
}
