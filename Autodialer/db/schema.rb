# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.1].define(version: 2025_11_10_035111) do
  create_table "articles", force: :cascade do |t|
    t.string "title"
    t.text "content"
    t.datetime "generated_at"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "blogs", force: :cascade do |t|
    t.string "title"
    t.text "content"
    t.datetime "generated_at"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "calls", force: :cascade do |t|
    t.string "phone_number", limit: 255, null: false
    t.string "status", limit: 255
    t.string "call_sid", limit: 255
    t.string "call_duration", limit: 255
    t.string "call_status", limit: 255
    t.text "error_message"
    t.datetime "called_at", precision: nil
    t.datetime "created_at", precision: nil, null: false
    t.datetime "updated_at", precision: nil, null: false
    t.index ["call_sid"], name: "index_calls_on_call_sid"
    t.index ["phone_number"], name: "index_calls_on_phone_number"
    t.index ["status"], name: "index_calls_on_status"
  end

end
