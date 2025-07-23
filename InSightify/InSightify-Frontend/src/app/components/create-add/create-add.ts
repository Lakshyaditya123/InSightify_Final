import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {FormBuilder, FormGroup, Validators, ReactiveFormsModule, FormsModule, FormControl} from '@angular/forms';
import { IdeaService } from '../../services/idea';
import { CurrUser, ApiResponse, RefineContent, TagsList, Add_idea} from '../../services/api-interfaces';
import { firstValueFrom } from 'rxjs';
import { AuthService } from '../../services/auth';
import { Editor, Toolbar, NgxEditorModule } from 'ngx-editor';

@Component({
  selector: 'app-create-add',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule, NgxEditorModule],
  templateUrl: './create-add.html',
  styleUrl: './create-add.css'
})
export class CreateAdd implements OnInit {
  addIdeaForm!: FormGroup;
  selectedFile: File | null = null;

  // newTagForm!: FormGroup;
  //State Management

  isSubmitting: boolean = false;
  isRefining: boolean=false;

  // Data holders
  selectedTags: TagsList[] = [];
  newTag:TagsList |null=null;
  Idea!:Add_idea;
  suggestedTags: TagsList[]=[];
  currentUserId!: number;
  currContent!:string;

editor!: Editor;
  toolbar: Toolbar = [
    ['bold', 'italic', 'underline', 'strike'],
    ['ordered_list', 'bullet_list'],
    [{ heading: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] }],
    ['text_color', 'background_color'],
    ['align_left', 'align_center', 'align_right', 'align_justify'],
  ];



  constructor(
    private fb: FormBuilder,
    private ideaService: IdeaService,
    private authService: AuthService
  ) {}


  ngOnInit() {
    this.initForm();
    this.editor = new Editor();
    // this.initNewTagForm();
    const currentUser: CurrUser | null = this.authService.getCurrentUser();
        if (currentUser) {
          this.currentUserId = currentUser.user_id;
    }
    this.Idea = {
      idea: {
        user_id: this.currentUserId,
        title: '',
        subject: '',
        content: '',
        link: null,
        file_path: null
      },
      refine_content: '',
      tags_list: []
    };
}

  initForm() {
    this.addIdeaForm = this.fb.group({
      title: ['', [Validators.required, Validators.maxLength(100)]],
      subject: ['', [Validators.required, Validators.maxLength(200)]],
      content: ['', Validators.required], // This was missing
      link: ['']
    });
  }
  // initNewTagForm() {
  //   this.newTagForm = this.fb.group({
  //     name: ['', Validators.required],
  //     description: ['']
  //   });
  // }
  // Add a new tag

  onFileSelected(event: Event): void {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files.length > 0) {
    this.selectedFile = input.files[0];
    console.log('Selected file:', this.selectedFile);
  }
}

  addTag(event: any) {
    event.preventDefault();
    const tag = this.newTag;
    if (tag && !this.selectedTags.includes(tag)) {
      this.selectedTags.push(tag);
      this.newTag=null;
    }
  }

  // Remove a tag
  removeTag(index: number) {
    this.selectedTags.splice(index, 1);
  }
  stripHtmlTags(html: string): string {
  if (!html) return '';
  
  // Remove HTML tags and common HTML entities
  let plainText = html
    .replace(/<[^>]*>/g, '') // Remove HTML tags
    .replace(/&nbsp;/g, ' ') // Replace non-breaking spaces
    .replace(/&amp;/g, '&')  // Replace HTML entities
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .trim();
  
  return plainText;
}
  // Add a suggested tag
  addSuggestedTag(tag: TagsList) {
    if (!this.selectedTags.includes(tag)) {
      this.selectedTags.push(tag);
    }
  }

  async refineIdea() {
    // const currentContent = this.addIdeaForm.get('content')?.value || '';
    let currentContent = this.addIdeaForm.get('content')?.value || '';

    const plainText = this.stripHtmlTags(currentContent);
    
    if (!plainText || plainText.length < 3) {
      alert('Please enter a description to refine.');
      return;
    }

    this.isRefining = true;
    this.currContent = currentContent; 

    try {
      const res: ApiResponse = await firstValueFrom(this.ideaService.refineIdea(plainText));
      if (res.errCode === 0 && res.datarec) {
        const refinedData: RefineContent = res.datarec;
        this.addIdeaForm.patchValue({ content: refinedData.refine_content });
        this.Idea.refine_content = refinedData.refine_content;
        this.suggestedTags = refinedData.tags_list;
        console.info('Content has been refined!', this.suggestedTags);
      } else {
        console.info('Failed to refine content.');
      }
    } catch (error) {
      console.error('Error refining idea:', error);
    } finally {
      this.isRefining = false;
    }
  }

  // Submit the form
  async submitIdea() {
    if (this.addIdeaForm.valid) {
      this.isSubmitting = true;
      try {
        const formValue = this.addIdeaForm.value;
        this.Idea.idea.user_id=this.currentUserId;
        this.Idea.idea.title=this.addIdeaForm.value.title;
        this.Idea.idea.subject=this.addIdeaForm.value.subject;
        this.Idea.idea.content=this.currContent;
        this.Idea.tags_list = this.selectedTags;
        // this.Idea!.idea.link=this.addIdeaForm.value.title;
        console.log('Submitting idea:', this.Idea);
        const res: ApiResponse = await firstValueFrom(this.ideaService.createIdea(this.Idea!));
        if(res.errCode==0){
          this.resetForm();
          this.closeModal();
        }
        else{
          alert("Error Submitting!")
        }

      } catch (error) {
        console.error('Error creating idea:', error);
      } finally {
        this.isSubmitting = false;
      }
    } else {
      this.markFormGroupTouched(this.addIdeaForm);
    }
  }

  // Reset the form
  resetForm() {
    this.addIdeaForm.reset();
    this.selectedTags=[];
    this.newTag = null;
    this.selectedFile = null;
    this.isSubmitting= false;
    this.isRefining=false;

  }

  // Mark all form controls as touched to show validation errors
  markFormGroupTouched(formGroup: FormGroup) {
    Object.values(formGroup.controls).forEach(control => {
      control.markAsTouched();
    });
  }

get contentControl(): FormControl {
  return this.addIdeaForm.get('content') as FormControl;
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