Rails.application.routes.draw do
  root "calls#index"
  
  # Blog routes
  get 'blog', to: 'blog#index'
  get 'blog/new', to: 'blog#new'
  post 'blog/generate', to: 'blog#generate'
  get 'blog/:id', to: 'blog#show', as: :blog_article
  delete 'blog/:id', to: 'blog#destroy'
  
  resources :calls, only: [:index, :create, :destroy] do
    collection do
      post :bulk_create
      post :start_calling
      post :ai_command
      post :upload_excel
      post :refresh_statuses
      get :logs
    end
  end
  
  get "up" => "rails/health#show", as: :rails_health_check
end
