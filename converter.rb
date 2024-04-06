#!/usr/bin/env ruby

require 'json'

ARGV.each do |file|
  next unless File.file?(file)
  
  questions = []
  File.readlines(file).each_slice(6) do |slice|
    question, correct, a, b, c, d = slice.map(&:strip)
    next unless question.start_with?("#Q")
    
    questions << {
      question: question[3..],
      correct: correct[1..],
      choices: {
        "A" => a[2..],
        "B" => b[2..],
        "C" => c[2..],
        "D" => d[2..]
      }
    }
  end

  File.write("#{file}.json", JSON.pretty_generate(questions))
end

