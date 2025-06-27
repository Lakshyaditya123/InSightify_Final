import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {FormBuilder, FormGroup, Validators, ReactiveFormsModule, FormsModule} from '@angular/forms';
import { Idea } from '../../services/idea';

@Component({
  selector: 'app-create-add',
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  templateUrl: './create-add.html',
  styleUrl: './create-add.css'
})
export class CreateAdd implements OnInit {
  addIdeaForm!: FormGroup;
  selectedTags: string[] = [];
  newTag: string = '';
  suggestedTags: string[] = [
    'AI', 'Web', 'Mobile', 'Health', 'Finance', 'Productivity'
  ];
  isSubmitting: boolean = false;

  constructor(
    private fb: FormBuilder,
    private ideaService: Idea
  ) {}

  ngOnInit() {
    this.initForm();
  }

  initForm() {
    this.addIdeaForm = this.fb.group({
      title: ['', [Validators.required, Validators.maxLength(100)]],
      subject: ['', [Validators.required, Validators.maxLength(200)]],
      content: ['', [Validators.required]]
    });
  }

  // Add a new tag
  addTag(event: any) {
    event.preventDefault();
    const tag = this.newTag.trim();

    if (tag && !this.selectedTags.includes(tag)) {
      this.selectedTags.push(tag);
      this.newTag = '';
    }
  }

  // Remove a tag
  removeTag(index: number) {
    this.selectedTags.splice(index, 1);
  }

  // Add a suggested tag
  addSuggestedTag(tag: string) {
    if (!this.selectedTags.includes(tag)) {
      this.selectedTags.push(tag);
    }
  }

  // Submit the form
  async submitIdea() {
    if (this.addIdeaForm.valid) {
      this.isSubmitting = true;

      try {
        const ideaData = {
          ...this.addIdeaForm.value,
          tags_list: [1],
          user_id: 2,

        };

        // Here you would call your backend API
        console.log('Submitting idea:', ideaData);

        // Mock API call - replace with actual service call
        const res :any= await this.ideaService.add_idea(ideaData).toPromise();
        if(res.error_code==0){
          alert('Submitted');
        }

        // Reset form and close modal
        this.resetForm();
        this.closeModal();

      } catch (error) {
        console.error('Error creating idea:', error);
      } finally {
        this.isSubmitting = false;
      }
    } else {
      this.markFormGroupTouched();
    }
  }

  // Reset the form
  resetForm() {
    this.addIdeaForm.reset();
    this.selectedTags = [];
    this.newTag = '';
  }

  // Mark all form controls as touched to show validation errors
  markFormGroupTouched() {
    Object.keys(this.addIdeaForm.controls).forEach(key => {
      const control = this.addIdeaForm.get(key);
      control?.markAsTouched();
    });
  }

  // Close the modal
  closeModal() {
    const modalElement = document.getElementById('addIdea_modal');
    if (modalElement) {
      const modal = (window as any).bootstrap.Modal.getInstance(modalElement);
      if (modal) {
        modal.hide();
      }
    }
  }

  // Get character count for description
  getDescriptionLength(): number {
    return this.addIdeaForm.get('description')?.value?.length || 0;
  }

  // Check if description is near limit
  isDescriptionNearLimit(): boolean {
    return this.getDescriptionLength() > 900;
  }



}
