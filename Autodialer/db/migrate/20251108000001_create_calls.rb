class CreateCalls < ActiveRecord::Migration[7.1]
  def change
    create_table :calls do |t|
      t.string :phone_number, null: false
      t.string :status, default: 'pending'
      t.string :call_sid
      t.string :call_duration
      t.string :call_status
      t.text :error_message
      t.datetime :called_at

      t.timestamps
    end
    
    add_index :calls, :phone_number
    add_index :calls, :status
    add_index :calls, :call_sid
  end
end
